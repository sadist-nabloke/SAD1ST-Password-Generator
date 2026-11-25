SAD1ST Password Generator — Android project

This is the project source plus a GitHub Actions workflow for cloud APK building.
It is NOT itself an APK.

Files:
- main.py: Kivy application source
- buildozer.spec: Buildozer configuration
- .github/workflows/android.yml: automatic cloud build workflow

BUILD THE APK USING ONLY YOUR PHONE
1. Sign in to GitHub in your phone browser and create a new repository.
   Choose a name such as SAD1ST-Password-Generator. Public or private is your choice.
2. Extract this ZIP on your phone.
3. Upload the project files and folders to the repository, keeping the folder structure.
   Important: the hidden .github folder must also be uploaded. If the GitHub mobile
   website hides it or makes uploading folders difficult, use github.dev in the browser
   after creating the repository, or upload the files from a ZIP using a GitHub-supported
   upload workflow.
4. Open the repository's Actions tab.
5. Select "Build Android APK" and tap "Run workflow" if it has not started automatically.
6. Wait for the workflow to finish successfully.
7. Open the completed workflow run, scroll to Artifacts, and download
   SAD1ST-Password-Generator-APK.
8. Extract the downloaded artifact ZIP and tap the APK to install it.
   Android may ask you to allow installation from that browser/file manager.

NOTES
- The first build can take several minutes.
- GitHub may require email verification before Actions can run.
- The workflow builds a debug APK, suitable for testing and personal installation.
- Password history is stored in the app's private local storage. Avoid saving passwords
  that you do not want retained on the device.
