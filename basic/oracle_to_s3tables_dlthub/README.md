# Context

This is a sample to illustrate how one can extract data from an Oracle database and load those into S3 Tables.

V1 will have the extraction from Oracle to the local file system.
In V2, the local file system will be replaced with S3 Tables.

## V1

1. set up a small Oracle database
2. load that Oracle database with some data
3. Extract data using a dlt pipeline.

## 🚀 Commands

We use [`uv`](https://github.com/astral-sh/uv) to manage Python dependencies efficiently. Here's how to get started:

### 🔧 Setup

1. **Install `uv`:**  
   ```bash
   brew install uv
   ```

2. **Create a virtual environment:**  
   ```bash
   uv venv .venv --python 3.11
   ```

3. **Activate the virtual environment:**  
   ```bash
   source .venv/bin/activate
   ```

4. **Install all dependencies:**  
   ```bash
   uv sync
   ```

5. **Add new libraries during development:**  
   ```bash
   uv add <library_name>
   ```

---

### ▶️ Running Pipelines

To run a specific pipeline script:

```bash
python <pipeline_file>.py
```

---

### 📊 Viewing Tables

To inspect the available tables in a pipeline:

```bash
dlt pipeline <pipeline_name> show
```
