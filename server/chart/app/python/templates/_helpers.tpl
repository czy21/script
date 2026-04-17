{{- define "app.fullname" -}}
{{- $name := .Values.fullnameOverride | default .Release.Name -}}
{{- $name -}}
{{- end -}}