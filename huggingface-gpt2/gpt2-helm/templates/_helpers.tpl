{{- define "gpt2-labels" -}}
app: {{ .Values.app.name }}
env: {{ .Values.app.env }}
{{- end -}}

{{- define "ingress-annotations" -}}
nginx.ingress.kubernetes.io/add-base-url: "true"
nginx.ingress.kubernetes.io/rewrite-target: /$2 
{{- end -}}