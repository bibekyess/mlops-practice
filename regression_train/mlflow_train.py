# Import packages
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import pandas as pd
import mlflow
from math import sqrt
from mlflow.client import MlflowClient
import time

# mlflow.set_tracking_uri("http://local-server/")
# Set the experiment name to an experiment in the shared experiments folder
mlflow.set_experiment("test")

client = MlflowClient()

# Set model name
name = 'DiabetesRegressionTask'

# Load the diabetes dataset
diabetes = datasets.load_diabetes()
diabetespd = pd.DataFrame(data=diabetes.data)

mlflow.end_run() # to end if any previous run is on
with mlflow.start_run() as run:
    # mlflow.autolog(log_models=True) # This is not supported in all model types

    diabetes_X = diabetes.data
    diabetes_y = diabetes.target
    diabetes_X_train, diabetes_X_test, diabetes_y_train, diabetes_y_test = train_test_split(diabetes_X, diabetes_y, test_size=0.25, random_state=42)

    alpha = 0.05
    solver = 'cholesky'

    # Log parameters
    mlflow.log_param('alpha', alpha)
    mlflow.log_param('solver', solver)

    # Log training dataset
    mlflow.log_input(mlflow.data.from_pandas(pd.DataFrame(data=diabetes_X_train, columns=diabetes.feature_names)), context="Training")
    # Log evaluation dataset
    mlflow.log_input(mlflow.data.from_pandas(pd.DataFrame(data=diabetes_X_test, columns=diabetes.feature_names)), context="Eval")

    regr = linear_model.Ridge(alpha=alpha,solver=solver)  

    regr.fit(diabetes_X_train, diabetes_y_train)
    diabetes_y_pred = regr.predict(diabetes_X_test)

    # Log model
    mlflow.sklearn.log_model(regr, "model")

    # Log desired metrics
    mlflow.log_metric("mse", mean_squared_error(diabetes_y_test, diabetes_y_pred))
    mlflow.log_metric("rmse", sqrt(mean_squared_error(diabetes_y_test, diabetes_y_pred)))
    mlflow.log_metric("r2", r2_score(diabetes_y_test, diabetes_y_pred))

    # Log tags
    mlflow.set_tag("data_source", "Diabetes dataset")
    mlflow.set_tag("model_type", "Ridge Regression")

    # Get the latest run_id which is generated above
    new_run_id = run.info.run_id

    # To get the run_id from the development stage
    # new_run_id = client.get_latest_versions(name, stages=["None"])[0].run_id

    new_run = client.get_run(new_run_id)
    new_metrics = new_run.data.metrics

    # Compare the recent run with the production run id and then stage to production if results is better
    try:
        prod_run_id = client.get_latest_versions(name, stages=["Production"])[0].run_id
    except:
        prod_run_id = None

    print(prod_run_id)
    if prod_run_id:
        prod_run = client.get_run(prod_run_id)
        prod_metrics = prod_run.data.metrics

        # Collate metrics into DataFrame for comparison
        columns = ['mse','rmse','r2']
        columns = ['version'] + [x for x in sorted(columns)]
        new_vals = ['new'] + [new_metrics[m] for m in sorted(new_metrics) if m in columns]
        prod_vals = ['prod'] + [prod_metrics[m] for m in sorted(prod_metrics) if m in columns]
        data = [new_vals, prod_vals]

        metrics_df = pd.DataFrame(data, columns=columns)

        new_mse = metrics_df[metrics_df['version'] == 'new']['mse'].values[0]
        new_rmse = metrics_df[metrics_df['version'] == 'new']['rmse'].values[0]
        new_r2 = metrics_df[metrics_df['version'] == 'new']['r2'].values[0]

        prod_mse = metrics_df[metrics_df['version'] == 'prod']['mse'].values[0]
        prod_rmse = metrics_df[metrics_df['version'] == 'prod']['rmse'].values[0]
        prod_r2 = metrics_df[metrics_df['version'] == 'prod']['r2'].values[0]

        # Check new model meets our validation criteria before promoting to production
        if (new_mse < prod_mse) and (new_rmse < prod_rmse) and (new_r2 > prod_r2):
            model_uri = f'{mlflow.get_artifact_uri()}/model'
            print('run_id is: ', new_run_id)
            
            desc = 'This model uses Ridge Regression to predict diabetes.'

            client.create_model_version(name, model_uri, new_run_id, description=desc)
            to_prod_version = client.search_model_versions("run_id='{}'".format(new_run_id))[0].version
            to_archive_version = client.search_model_versions("run_id='{}'".format(prod_run_id))[0].version
            
            # Transition new model to Production stage
            client.transition_model_version_stage(name, to_prod_version, "Production")
            
            # Wait for the transition to complete
            new_prod_version = client.get_model_version(name, to_prod_version)
            while new_prod_version.current_stage != "Production":
                new_prod_version = client.get_model_version(name, to_prod_version)
                print('Transitioning new model... Current model version is: ', new_prod_version.current_stage)
                time.sleep(1)

            # Transition old model to Archived stage
            client.transition_model_version_stage(name, to_archive_version, "Archived")

        else:
            print('no improvement')
        