# Google Play Data Extraction & Integration Pipeline

This document outlines the process for extracting game metrics from the Google Play Developer Console, organizing the data, and automating the upload to Google Sheets for further analysis and modeling.

---

## 1. Data Extraction from Google Play

There are two primary ways to retrieve data: manual exports for quick checks and CLI-based exports for automation.

### A. Manual Export (CSV)
For one-off reports or manual validation of game metrics:
*   **Statistics:** Navigate to **Statistics** in the left menu. Configure your metrics (e.g., App gains, Store listing visitors), and click the **Export** button at the top right of the chart.
*   **Financials:** Go to **Download reports > Financial** to download monthly earnings and estimated sales reports directly.

### B. Google Cloud CLI Tool (Automated)
To automate the download of large datasets, use the [Google Cloud SDK](https://docs.cloud.google.com/sdk/docs/install-sdk).

#### 1. Authentication
Initialize the SDK and authenticate your account:
```bash
gcloud init
gcloud auth application-default login
```
After authentication, reload your shell configuration to apply changes:
```bash
source ~/.zshrc
```

#### 2. Locate your Bucket ID
1.  Log in to the [Google Play Console](https://play.google.com/console/).
2.  Go to **Download reports** (under "Quality" or "Grow").
3.  Select any report category (e.g., **Statistics**).
4.  Click **Copy Cloud Storage URI** near the top of the page.
5.  The URI looks like `gs://pubsite_prod_rev_01234567890123456789`. Your **Bucket ID** is the string starting with `pubsite_prod_rev_`.

#### 3. Extract Data
Run the following command to download reports for a specific app:
```bash
gcloud storage cp "gs://pubsite_prod_rev_<BUCKET_ID>/<APP_BUNDLE_ID>/*" ./reports/
```
*Replace `<BUCKET_ID>` and `<APP_BUNDLE_ID>` with your specific identifiers.*

---

## 2. Data Organization & Compilation

Once the CSVs are downloaded, partition them into logical folders to prepare for the upload process.

```bash
# Create directories for different metrics
mkdir crashes installs ratings

# Move files based on naming patterns
mv "*crashes*" crashes/
mv "*installs*" installs/
```

---

## 3. Uploading to Google Sheets

We use the Google Sheets API v4 to automate the transition from local CSVs to a cloud-based database.

### Prerequisites: Google Cloud Setup
1.  **Create a Project** in the [Google Cloud Console](https://console.cloud.google.com/).
2.  **Enable APIs:** Enable both the **Google Sheets API** and **Google Drive API**.
3.  **Service Account:**
    *   Create a Service Account under **Credentials**.
    *   Download the **JSON Key file**. **Keep this file secure!**
4.  **Share the Sheet:** Open your target Google Sheet and "Share" it with the `client_email` found in your JSON credentials (give it **Editor** access).

### Environment Setup
Install the required Python libraries:
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Execution
Use the following script to upload folders sequentially to your spreadsheet:
*   **Script:** [upload_to_sheets.py](./upload_to_sheets.py)

---

## 4. Database Integration & Cleanup

### Data Merging
Combine information into a single master database by linking the main sheet to the individual metric sheets within your Google Sheet document.

### Data Cleanup & Normalization
Google Play reports often omit rows for days with zero activity (e.g., zero crashes or zero ratings). These gaps must be filled before feeding data into models.

1.  **Missing Rows:** Use the cleanup script to inject missing dates into the sequence.
2.  **Ratings Smoothing:** For days with no new ratings, the average rating might appear as `NA`. To fix this, we use the **cumulative average rating** from the previous available data point.

---
**Next Step:** Once cleanup is complete, the data is ready for model training and inference.
