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

## Streamlit Setup

### Running locally
    
   To run locally (default Local URL: [http://localhost:8501](http://localhost:8501))
   ```
   streamlit run membership.py
   ```

### Deploy on streamlit

   One option to deploy for free is [Streamlit.io](https://streamlit.io/)
> **Warning**
> 
> To deploy on Streamlit Cloud, repo  MUST be public unless it is your ONE free private app. To replicate this app's setup, take below steps to protect your data & add some admittedly minimal authentication.

> :memo: **Tips**
>   * Start with relatively simple app setup. 
>   * Then use [secrets management](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management) and [caching](https://docs.streamlit.io/library/advanced-features/caching) to layer in options.
>   * Test connections & configurations locally `.streamlit/secrets.toml` before deploying
>   * :warning: Update `.gitignore` to protect secrets.
>   * Add to production by going to the app dashboard and in the app's dropdown menu, click on **Edit Secrets**. Copy the content of `secrets.toml` into the text area.

> **Note**
>  * Layer in new connections & configurations gradually.
>  * Add them locally & then again in deployment.
>  * If you want until everything works locally before deployment, it might still fail, and it will be MUCH harder to debug.
>  * If app deployed & you are app owner, you can debug deployment in **Manage App** tab in bottom right corner of app.     

1. Make repo public. :warning: CAREFUL
2. Deploy on [Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)
3. Add users & passwords [authentication without SS0](https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso).
4. Connect to datasource(s) using secrets management and caching. Check out [tutorials](https://docs.streamlit.io/knowledge-base/tutorials/databases).


### This app uses Private Google Sheet option
> **Note**
>
> `google.oauth2` not working in `virtualenv`. Continuing to dev outside virtualenv.

> **Note**
>
>  Streamlit tutorial points to deprecated and limited python library to interface with Google Sheets. [`gspread`](https://docs.gspread.org/en/latest/) is a great alternative!

# Linking Data

## Private Google Sheet FTW!
   - Easy, accessible
   - Great for keeping everything in house
>  **Warning**
>  Transfer to another party would take several not so straightforward steps.
>  Alternative DB solutions are potentially better for clients & external partners
   1. link via steps... (see above)
   2. revoke assess to sheet from everyone. limit to authorized users
   3. add service email to authorise email - VIEW ONLY!
   4. separate sheets in same doc can be linked to as unique urls. makes things contained   
>   **Note** 
>   Everything in `secrets.toml` accessible by others in your org. Secrets are not exactly secret there.

## User & passwords
>   **Note** 
>   Everything in `secrets.toml` accessible by others in your org. Secrets are not exactly secret there.
1. Logic checks if there's username in sheet & if there is a username password match 

## Workday employee data
1. Import directly into private google sheet using custom AppScript. Thank you, @bradspar, for [your example](https://github.com/bradjasper/ImportJSON) that uses Basic Auth and doesn't break!!
2. More info on source can be found by reaching out to in to tech team for authorization. **HINT**: There's a **Workday - Airtable Reports** document with all the necessary details.
> **Note** 
> reading data from Google Sheets changes the default datatypes and some columns name formats might need extras handling.

## Member data
- Defined by Slack channel membership currently. Limited in that they are only snapshot lists.
1. Go to settings of Slack channel
2. Copy member emails
3. Examples can be entered manually user into app
> **Note** 
> To add into backend of app takes some coding. 