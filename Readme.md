# OpenShift Deployment Steps

## Step 2: Log in to OpenShift and Create a Project
Use the oc command-line tool to log into your cluster and create a new project for the application.

### Log in to your OpenShift Cluster
```
oc login --token=<YOUR_TOKEN> --server=<YOUR_SERVER_URL>
```

### Create a new project
```
oc new-project report-viewer-app
```

## Step 3: Create a Secret for ODF Credentials
Store your sensitive ODF keys in a Secret rather than in plain text.

### Encode your keys in Base64
```
echo -n '<ODF_ACCESS_KEY>' | base64
echo -n '<ODF_SECRET_KEY>' | base64
```

### Update `odf-secret.yaml` with the encoded output secrets.
```
ODF_ACCESS_KEY: <ENCODED_ODF_ACCESS_KEY>
ODF_SECRET_KEY: <ENCODED_ODF_SECRET_KEY>
```

### Apply the secret
```
oc apply -f odf-secret.yaml
```

## Step 4: Update and Apply the Deployment YAML
Review and update the `openshift-deployment.yaml` file defines all the necessary OpenShift resources to build, deploy, and expose your application.

## Step 5: Apply the YAML and Start the Builds

### Apply the deployment configuration
```
oc apply -f openshift-deployment.yaml
```

### Manually start the builds
OpenShift will pull the code, build the container images using the Dockerfiles, and store them in its internal registry.
```
oc start-build report-viewer-backend-build
oc start-build report-viewer-frontend-build
```

### Monitor the builds and deployment
Watch the build logs
```
oc logs -f build/report-viewer-frontend-build-1
```

Watch the pods until they are 'Running'
```
oc get pods -w
```

## Step 6: Access Your Application
Once the pods are running, find the public URL assigned to your application's Route.

```
oc get route report-viewer
```

Open the URL provided in the HOST/PORT column in your web browser. You can now use the web interface to upload and view reports stored in your ODF bucket.
