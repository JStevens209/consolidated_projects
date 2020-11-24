### Overview

work-in-progress

### Google Kubernetes Engine (GKE)

The initial CLI setup is done after the cluster is created on CKE (see, [GKE Quickstart](https://cloud.google.com/kubernetes-engine/docs/quickstart))

```
$ gcloud config set project powerful-genre-237220
$ gcloud config set compute/zone us-central1-a
$ gcloud container clusters get-credentials gnosko-cluster-1
```

### j2

```
$ pip install j2cli
```
