# vet_clinic
This is my homework and practice on the FastAPI framework.

## What's that?

A simple example of FastAPI framework usage.

Let's imagine that somebody asked us to make a webservice for a vet clinic. The statement of work with all the functionality we need to provide is inside the [clinic.yaml](clinic.yaml) file. You can check it with [swagger editor](https://editor-next.swagger.io/) for more details. I'm not using any database, the "database" is imitated by dict and list inside the code.

**What can it do?**

- @POST on '/post': post current timestamp and assign primary key to it;
- @GET on '/dog': get the dog by its kind (or get all the dogs if kind is not specified);
- @POST on '/dog': post new dog entry to the "database";
- @GET on '/dog/{pk}': get the dog by its primary key;
- @PATCH on '/dog/{pk}': patch the dog entry by the primary key.

## Author

[Me](@onthebox)
