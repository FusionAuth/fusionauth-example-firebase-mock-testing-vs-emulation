# Example testing Firebase services with Mocking vs Emulation

Example repo for the Why mocking sucks post illustrating testing Firebase services with mocking vs with the Firebase emulator.

## Prerequisites

- [Python](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv)


## Getting Started

Create a Firebase project and download your service account key file from your project configuration. Paste the contents of the service account key into the `service_account_key_example.json` file.


### Test with Mocking 

Use the following command to run mocked tests

```sh
uv run pytest firebase_test_with_mocking.py
```


### Test with Firebase Emulation


Install the Firebase CLI.

```sh 
npm install -g firebase-tools
```

Authenticate the CLI

```sh
firebase login
```

Initialize the project. 

```sh
firebase init
```

Initialize Firebase Emulators.

```sh 
firebase init emulators
```

Start the emulator.

```sh
firebase emulators:start
```

Run the test against the emulator

```sh
uv run pytest firebase_test_with_emulator.py
```