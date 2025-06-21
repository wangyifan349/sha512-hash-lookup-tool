# SHA512 Hash Lookup Tool 🔍🔐

Welcome to the **SHA512 Hash Lookup Tool**! This project helps you quickly identify the original strings or files based on their SHA-512 hashes. It is designed to prevent tampering by relying on secure cryptographic hash verification.

---

## 🚀 Features

- **SHA-512 Hashing:** Uses SHA-512 hashes to ensure data integrity and prevent tampering.
- **String & File Lookup:** Query hashed values to find the original strings or corresponding file paths.
- **Batch File Scan:** Automatically scans a specified directory for files and indexes their SHA-512 hashes.
- **User-friendly Web Interface:** Beautiful dark mode UI with red accents for comfortable viewing.
- **Secure Input Validation:** Validates input to accept only valid SHA-512 hash strings (128 hex characters).
- **Lightweight Python/Flask backend:** Easy to run and customize.

---

## 🛠️ How It Works

To prevent tampering or unauthorized modifications, files and known strings are registered by their SHA-512 hashes. When you provide a SHA-512 hash, the tool looks up if it corresponds to any pre-stored strings or scanned files. This helps you quickly verify data integrity or identify the content behind a secure hash.

---

## 📂 Use Cases

- **Verify file authenticity:** Compare files on your system to known hashes to detect alterations.
- **Look up hashed strings:** Identify original strings from their SHA-512 hashes in your projects.
- **Quick hash-based content verification:** Useful for security audits, checksums, or cryptographic investigations.

---

## ⚙️ Setup & Run

1. Clone the repository:
    ```bash
    git clone https://github.com/wangyifan349/sha512-hash-lookup-tool.git
    cd sha512-hash-lookup-tool
    ```

2. Install dependencies:
    ```bash
    pip install flask
    ```

3. Prepare files to scan:
    - Place any files you want to index by their SHA-512 hashes inside the folder `files_to_check` (create if not exists).

4. Run the application:
    ```bash
    python app.py
    ```

5. Open your browser and go to:
    ```
    http://127.0.0.1:5000/
    ```

---

## 🔐 Security Note

- SHA-512 is a cryptographic hash function designed to be collision-resistant.
- This tool leverages SHA-512 hashing to help **detect data tampering** reliably.
- It is not a replacement for encryption; original data is never revealed unless matched.
- Input hashes are validated strictly to ensure correct query formats.

---

## 🎨 UI

The interface uses a **dark theme with red accents** to provide a comfortable, eye-friendly experience during prolonged use.

---

## 🤝 Contribution

Feel free to fork, submit issues, or create pull requests! Your feedback and contributions are welcome.

---

## 📫 Contact

GitHub: [https://github.com/wangyifan349](https://github.com/wangyifan349)

---

### Thank you for using the SHA512 Hash Lookup Tool! 💻🔎🔐
