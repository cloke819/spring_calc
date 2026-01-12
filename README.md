# Spring Calc Streamlit App

Minimal Streamlit app for spring calculations. To run locally and deploy, follow the steps below.

## Run locally
1. Install Python 3.8+.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run spring_calc.py
```

## Publish to GitHub
1. Install Git (see next section) or use GitHub Desktop.
2. Initialize repo, commit, and push to GitHub (replace `<your-repo-url>`):

```bash
git init
git add .
git commit -m "Initial commit: add spring_calc Streamlit app"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## Deploy to Streamlit Community Cloud
1. Sign in at https://share.streamlit.io with your GitHub account.
2. Click "New app", select your repository and branch `main`, and set the main file to `spring_calc.py`.
3. Click "Deploy" and share the generated URL with colleagues.

## Installing Git on Windows
- Option A (recommended): Download and run installer from https://git-scm.com/download/win
- Option B: Use `winget`:

```powershell
winget install --id Git.Git -e --source winget
```

After installing, verify with:

```powershell
git --version
```

If `git` still isn't recognized, restart your terminal or sign out/sign in to update PATH.

---
If you'd like, I can initialize the local git commit messages in this folder and show the exact commands to run after you install Git.
