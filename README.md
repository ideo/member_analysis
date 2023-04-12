# member_analysis

## Python Setup
1. Create a virtual environment of your choosing. Below is a pyenv example. To truly understand the magic of pyenv (which helps you manage multiple versions of python!) check out these install & setup [instructions](https://realpython.com/intro-to-pyenv/) (see the **Installation** section of [this page](https://gist.github.com/eliangcs/43a51f5c95dd9b848ddc) for help)

    To create virtualenv:
    ```
    pyenv virtualenv 3.8.7 members
    ```

    To activate virtualenv:
    ```
    pyenv activate members
    ```

    To deactivate virtualenv:
    ```
    source deactivate
    ```

## Running locally
    
   To run locally (default Local URL: [http://localhost:8501](http://localhost:8501))
   ```
   streamlit run membership.py
   ```

## Deploy on streamlit

   One option to deploy for free is [Streamlit.io](https://streamlit.io/)
> **Warning**
> 
> To deploy on Streamlit Cloud, repo  MUST be public unless it is your ONE free private app. To replicate this app's setup, take below steps to protect your data & add some admittedly minimal authentication.

1. Make repo public. :warning: CAREFUL

   **TIPS**
   * Start with relatively simple app setup. 
   * Then use [secrets management](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management) and [caching](https://docs.streamlit.io/library/advanced-features/caching) to layer in options.
   * Test connections & configurations locally `.streamlit/secrets.toml` before deploying
   * :warning: Update `.gitignore` to protect secrets.
   * Add to production by going to the app dashboard and in the app's dropdown menu, click on **Edit Secrets**. Copy the content of `secrets.toml` into the text area.
> **Note**
>  * Layer in new connections & configurations gradually.
>  * Add them locally & then again in deployment.
>  * If you want until everything works locally before deployment, it might still fail, and it will be MUCH harder to debug. 

2. Deploy on [Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)
3. Add users & passwords [authentication without SS0](https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso).
4. Connect to datasource(s) using secrets management and caching. Check out [tutorials](https://docs.streamlit.io/knowledge-base/tutorials/databases).