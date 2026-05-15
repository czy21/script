{{- define "app.fullname" -}}
{{- $name := .Values.fullnameOverride | default .Release.Name -}}
{{- $name -}}
{{- end -}}

{{- define "app.image" -}}
{{- if and .Values.param_release_image (ne .Values.param_release_image "") }}
{{- .Values.param_release_image }}
{{- else }}
{{- printf "%s/%s/%s:%s"
    .Values.param_registry
    .Values.param_registry_dir
    (include "app.fullname" .)
    .Values.param_release_version }}
{{- end }}
{{- end }}