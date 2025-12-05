# Visualisasi Maximum Clique Problem (Bron-Kerbosch)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Pygame](https://img.shields.io/badge/Library-Pygame-green.svg)

Aplikasi visualisasi interaktif untuk memahami **Maximum Clique Problem** menggunakan algoritma **Bron-Kerbosch**. Dibuat dengan Python dan Pygame, aplikasi ini dirancang untuk tujuan edukasi dengan fitur langkah-demi-langkah, penjelasan naratif, dan tampilan modern.

---

## 🇮🇩 Bahasa Indonesia

### Fitur Utama
- **Visualisasi Algoritma**: Melihat bagaimana algoritma Bron-Kerbosch bekerja mencari clique terbesar secara real-time.
- **Mode Edukasi (Step-by-Step)**:
  - **Panel Pseudocode**: Menyorot baris kode yang sedang dieksekusi.
  - **Narasi Penjelasan**: Penjelasan logika langkah demi langkah dalam Bahasa Indonesia.
  - **Recursion Stack**: Memvisualisasikan tumpukan pemanggilan fungsi rekursif.
- **Dual Mode**:
  - **Quick Run**: Mendapatkan hasil instan.
  - **Step Run**: Mode belajar dengan kecepatan yang bisa diatur atau manual.
- **Interaktif**: Buat graf sendiri dengan klik mouse atau gunakan generator **Random Graph**.
- **Modern UI**: Tampilan antarmuka yang bersih dan modern (Dark Mode).

### Prasyarat
- Python 3.x
- Library `pygame` dan `numpy`

### Cara Menjalankan
1. Install library yang dibutuhkan:
   ```bash
   pip install pygame numpy
   ```
2. Jalankan program:
   ```bash
   python max_clique_visualizer.py
   ```

### Kontrol
- **Klik Kiri (Area Kosong)**: Tambah Node.
- **Klik Kiri (Node ke Node)**: Tambah/Hapus Garis (Edge).
- **Klik Kanan (Node)**: Hapus Node.
- **Tombol UI**:
  - **RANDOM GRAPH**: Membuat graf acak.
  - **QUICK RUN**: Jalankan instan.
  - **STEP RUN**: Jalankan mode visualisasi.
  - **PAUSE / RESUME**: Jeda visualisasi.
  - **NEXT STEP**: Maju satu langkah (saat di-pause).
  - **RESET**: Hapus semua.

---

## EN English

### Key Features
- **Algorithm Visualization**: See the Bron-Kerbosch algorithm in action finding the maximum clique in real-time.
- **Educational Mode (Step-by-Step)**:
  - **Pseudocode Panel**: Highlights the exact line of code being executed.
  - **Narrative Explanation**: Step-by-step logic explanation (currently in Indonesian).
  - **Recursion Stack**: Visualizes the recursive function call stack.
- **Dual Mode**:
  - **Quick Run**: Get instant results.
  - **Step Run**: Learning mode with adjustable speed or manual stepping.
- **Interactive**: Build your own graph by clicking or use the **Random Graph** generator.
- **Modern UI**: Clean and modern Dark Mode interface.

### Requirements
- Python 3.x
- `pygame` and `numpy` libraries

### How to Run
1. Install dependencies:
   ```bash
   pip install pygame numpy
   ```
2. Run the script:
   ```bash
   python max_clique_visualizer.py
   ```

### Controls
- **Left Click (Empty Area)**: Add Node.
- **Left Click (Node to Node)**: Add/Remove Edge.
- **Right Click (Node)**: Delete Node.
- **UI Buttons**:
  - **RANDOM GRAPH**: Generate a random graph.
  - **QUICK RUN**: Instant execution.
  - **STEP RUN**: Visualization mode.
  - **PAUSE / RESUME**: Pause visualization.
  - **NEXT STEP**: Advance one step (when paused).
  - **RESET**: Clear all.
