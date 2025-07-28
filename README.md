# AERORENT UK Website

A modern, responsive website for AERORENT UK aircraft rental services, deployed on Streamlit Community Cloud.

## Features

- 🛩️ Premium aircraft rental services
- 🚁 Helicopter services
- ✈️ Commercial aircraft charters
- 📱 Responsive design
- 🎨 Modern UI/UX

## Local Development

To run this website locally:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. Open your browser and go to `http://localhost:8501`

## Deployment to Streamlit Community Cloud

### Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it something like `aerorent-uk-website`
3. Make it public (required for Streamlit Community Cloud)

### Step 2: Push Your Code to GitHub

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: AERORENT UK website"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/aerorent-uk-website.git

# Push to GitHub
git push -u origin main
```

### Step 3: Deploy to Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `YOUR_USERNAME/aerorent-uk-website`
5. Set the main file path: `app.py`
6. Click "Deploy"

Your website will be available at: `https://YOUR_APP_NAME-YOUR_USERNAME.streamlit.app`

## Customization

- Edit `index.html` to modify the website content and styling
- Update `app.py` to change Streamlit app behavior
- Modify `requirements.txt` to add additional dependencies

## File Structure

```
├── app.py              # Streamlit application
├── index.html          # Main HTML website
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Support

For any issues or questions, please contact the development team. 