---
title: "Scraping web sites and unstructured data"
description: "Making the best of data from the internet and bad, ugly data from PDFs"
order: 1
data_files:
  - nyc-documents/*
  - procurement-sample/*
links:
    - url: https://jsoma.github.io/easy-scraper-modified/
      name: Easy Scraper (modified)
      description: Chrome extension for scraping – modified by me to make it work in more cases
    - url: https://prishtinaonline.com/prokurimi/njoftim-per-kontrate
      name: Procurement contracts
    - url: https://www.pak-ks.org/page.aspx?id=1%2C106
      name: Bid document listing
      description: (in Albanian, because it has more than the English version)
    - url: https://web.archive.org/web/20121116220124/http://www.coloribus.com/focus/outdoor-ads-as-monuments-sculptures-stunts-installations-statues/11933155/
      name: Outdoor ads as monuments, sculptures, stunts, installations, statues
      description: A resource from the NEWBORN monument's Wikipedia page
    - url: https://motrix.app/
      name: Motrix
      description: A great app for downloading things
    - url: https://chromewebstore.google.com/detail/bulk-pdf-downloader-%E2%80%93-dow/flpckiejbjlkjgfohcoognkaogiacjnh
      name: Bulk PDF Downloader
      description: Chrome extension for downloading all of the PDFs linked on a page
    - url: https://docs.google.com/spreadsheets/d/1JcVNQEBVLCoeQo8pbdm4OjDsaskB7FMzM_r83t224FA/edit?usp=sharing
      name: Claude for Sheets example spreadsheet
    - url: https://github.com/yt-dlp/yt-dlp
      name: yt-dlp
      description: A Python library for downloading videos on the internet
    - url: https://github.com/openai/whisper
      name: Whisper
      description: A Python library for transcribing audio and video
    - url: https://s7.stacher.io/
      name: Stacher
      description: A tool for downloading YouTube videos without code
    - url: https://pulitzercenter.org/misinformation-tiktok-how-documented-examined-hundreds-videos-different-languages
      name: Misinformation on TikTok
      description: How 'Documented' Examined Hundreds of Videos in Different Languages

---

## Intro

Scraping is a powerful way to convert web sites into data files that you can analysis with Sheets, Excel, or even ChatGPT.

## Using NotebookLM

Visit [https://notebooklm.google.com/](NotebookLM) and create a **new notebook**.

![](notebooklm-new.png)

Upload your files.

![](notebooklm-upload.png)

Ask your question.

![](notebooklm-question.png)


## Using Easy Scraper

After you've [installed Easy Scraper](https://jsoma.github.io/easy-scraper-modified/), you first need to open it by clicking the extensions button.

![](easyscraper-open.png)

Then you might need to click "Change List" until the rows look reasonably right. Don't worry if there's extra stuff in there, you can clean it up later.

![](easyscraper-pick.png)

Are there **multiple pages?** Pick an option from the dropdown.

![](easyscraper-next-1.png)

If there's a "Next" button: you'll pick **Click link to navigate to next page**, then **Select**, then click the "Next" button.

![](easyscraper-next-2.png)

Time to **Start scraping!**

![](easyscraper-start.png)

It'll go and go and go and go and go. When you want to be done, click **Stop Scraping**.

<video width="100%" height="auto" autoplay loop muted playsinline>
  <source src="easyscraper-scraping.mov">
</video>

And in the end, export with the **CSV** button.

![](easyscraper-download.png)

## Running code in Colab

### Getting some code

If you have a CSV that you want Colab to analyze, open up your CSV in Google Sheets or Excel. **You'll need to paste a few rows into your conversation so ChatGPT knows what your data looks like.**

Explain what you want to ChatGPT. Let's say you asked me, "I want to explore the data" and I said "there's a nice graphing library called Altair that will do that for you"

> [Here's my example](https://chatgpt.com/share/68ae8bc9-2b8c-800d-a701-2ad4e8633c11)
>
> I have the following data in amazon-2025-08-27.csv, i want to analyze it in Google Colab and make an interactive Altair graphic that plots the price per pound vs number of stars.
>
> (paste a few rows of data)

**Be as descriptive as possible**. You'll get some code back.

### Using the code

Then, visit [Google Colab](https://colab.research.google.com/) and create a **New Notebook**.

![](colab-new.png)

To be need to use a file (like your CSV, if you have one), click **Run all** to make the notebook start, then click the **Folder button** on the left-hand side.

![](colab-upload-1.png)

Now you can use the Upload icon or drag-and-drop files in.

<video width="100%" height="auto" autoplay loop muted playsinline>
  <source src="colab-upload-2.mov">
</video>

**To run your code:** you'll copy the code [from the ChatGPT conversation](https://chatgpt.com/share/68ae8bc9-2b8c-800d-a701-2ad4e8633c11) and put it into your notebook. Use the **+ Code** button to add new blocks of code, and **►** Play button to run your code.

![](copy-code-1.png)

![](copy-code-2.png)

And then you'll be good to go! 

### Downloading "clean" data

If you want to clean your data or download a file analysis, **just ask ChatGPT**. It can give you code to create new, clean CSV files and download them to your computer from Colab.

> Provide code to fully clean the file and download it as something nice I can give a data person. I'm in Google Colab.

## Exercises

### Scraping monuments

[This website](https://web.archive.org/web/20121116220124/http://www.coloribus.com/focus/outdoor-ads-as-monuments-sculptures-stunts-installations-statues/11933155/) is awful looking. Can you use Easy Scraper to grab them as a CSV?

### Analyzing Airbnb

1. Visit [Airbnb](https://www.airbnb.com/) for a given region. Search for some time in the future.
2. Scrape the results
3. Find the number of apartments and average cost in each city

### Analyzing a YouTube channel

1. Visit a [Youtube channel](https://www.youtube.com/@joerogan) popular in your country.
2. Ask ChatGPT for code using yt-dlp to download the most recent 10 videos from a specific account or playlist, then to transcribe it using Python Whisper's  "turbo" version and download the results as a CSV file.
3. Upload it into Google Sheets and use Claude for Sheets to summarize or analyze each transcript.

### Analyzing procurement data

*Are there any Pristina procurement contracts that have to do with animals that live on the street?*

If you're feeling fancy, scrape the list of [procurement data for Prishtina](https://prishtinaonline.com/prokurimi/njoftim-per-kontrate) and download them all (or some of them, probably) using [Motrix](https://motrix.app/). You can also just use the ones in this session's download materials (the **procurement-sample** folder.)

### More procurement

We can't answer questions like "what is the largest contract" without converting the procurement data into structured data.

If you're feeling lazy, use the "procurement documents" tab in the [Claude for Sheets example spreadsheet](https://docs.google.com/spreadsheets/d/1JcVNQEBVLCoeQo8pbdm4OjDsaskB7FMzM_r83t224FA/edit?gid=1292642224#gid=1292642224). I already organized it for you!

But if you're feeling very charged up, [here's how I did it for exactly one file](https://colab.research.google.com/github/jsoma/2025-birn/blob/main/unstructured-data/procurement-sample-analysis.ipynb), can you talk to ChatGPT to make it work for the rest?