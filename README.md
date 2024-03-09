# Tugas-Besar-Strategi-Algoritma-2024-Jadi-Mesin

<!--
i. Penjelasan singkat algoritma greedy yang diimplementasikan
ii. Requirement program dan instalasi tertentu bila ada
iii. Command atau langkah-langkah dalam meng-compile atau build
program
iv. Author (identitas pembuat)
-->

## Deskripsi Tugas Besar Pemanfaatan Algoritma Greedy dalam Pembuatan Bot Permainan Diamonds

Pada tugas pertama Strategi Algoritma ini, dibuat sebuah bot yang nantinya akan dipertandingkan satu sama lain. Bot tersebut akan menggunakan strategi greedy dalam melakukan pergerakan. Secara singkat dan sederhana, strategi greedy yang kami gunakan adalah memilih diamond berdasarkan density terbesar. Pada kasus ini, density yang dimaksud adalah nilai bobot diamond dibagi dengan jarak diamond. Tentunya kami juga  memastikan bahwa diamond yang menjadi solusi harus bisa diambil dengan mempertimbangkan komponen-komponen game lain seperti bot musuh, tombol merah, base, dan teleportasi.

Berikut adalah deskripsi Program permainan Diamonds: 
1. Game engine, yang secara umum berisi: 
Kode backend permainan, yang berisi logic permainan secara keseluruhan serta API yang disediakan untuk berkomunikasi dengan frontend dan program bot 
Kode frontend permainan, yang berfungsi untuk memvisualisasikan permainan 

2. Bot starter pack, yang secara umum berisi: 
Program untuk memanggil API yang tersedia pada backend 
Program bot logic (bagian ini yang akan kalian implementasikan dengan algoritma greedy untuk bot kelompok kalian) 
Program utama (main) dan utilitas lainnya 


## Table of Contents

- [General Info](#general-information)
- [Team Members](#team-members)
- [How to Run](#how-to-run)
- [Program Structure](#program-structure)

## General Information

```
<ISI INFORMASI>
```

## How to Run

1. Install Requirements:

- Python 3 (https://www.python.org/downloads/)
- Node.js (https://nodejs.org/en)
- Docker desktop (https://www.docker.com/products/docker-desktop/)
- Yarn
  ```
  npm install --global yarn
  ```

2. Clone this repository.

```
$ git clone https://github.com/PanjiSri/Tubes1_JadiMesin.git
```

3. Open GNU Prolog Console and change working directory using `change_directory('directory').`. Navigate to `src` folder.

4. Consult `initiate.pl` file using `consult('initiate.pl').` in GNU Prolog Console.

5. Run initiate.pl with the argument below

```
$ startGame.
```

## Team Members

| **NIM**  |        **Nama**         |
| :------: | :---------------------: |
| 13521013 | Panji Sri Kuncara Wisma |
| 13521041 |   Ahmad Hasan Albana    |
| 13521042 |      Amalia Putri       |

## Program Structure

```
.
│   README.md
|
└───doc
|   └───Progress1_G03.pdf
|       Progress2_G03.pdf
|       Laporan_G03.pdf
|
└───src
    |
    └───attack.pl
        dynamicfacts.pl
        initiate.pl
        map.pl
        player.pl
        risk.pl
        rules.pl
        staticfacts.pl
        troops.pl
        turn.pl
        utilities.pl
        wilayah.pl
```
