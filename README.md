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
> ⚠️ **Warning** ⚠️
> 
> To deploy on Streamlit Cloud, repo  MUST be public unless it is your ONE free private app. To replicate this app's setup, take below steps to protect your data & add some admittedly minimal  [authentication without SS0 using secrets management](https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso).

1. Add users & passwords locally in `.streamlit/secrets.toml` & ⚠️ update `.gitignore` ⚠️
