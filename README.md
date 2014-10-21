## Block Page Detection Code

This repo contains similarity metrics to evaluate how similar two web
pages are. This code can be applied to a test page and a known good
version of the page to determine if the test page is a block page.

Using the thresholds from our
[IMC 2014 Short Paper](http://conferences2.sigcomm.org/imc/2014/papers/imc2014-shortpaper46.pdf), we were able to detect block pages with 95% accuracy and 80% precision.

## Running the code

To compare two files, run: `./similarityMetrics.py <FILE 1> <FILE 2>`

If the given filenames contain "HTTP://", the code will assume that you
want to download the website and compare the downloaded content.

Therefore, you can compare Google.com to itself with
`./similarityMetrics.py http://www.google.com http://www.google.com`

## Detection Thresholds from the Paper

Similarity Measure  | True Positive/ Recall (%)  | False Positive (%)  | Precision (%)  | Threshold
------------------- | -------------------------- | ------------------- | -------------- | ----------
Page Length | 95.03 ±1.128 · 10−3 | 1.371 ±1.829 · 10−16 | 79.80 ±1.915 · 10−4 | 30.19%
Cosine Similarity | 97.94 ±2.341 · 10−14 | 1.938 ±3.657 · 10−16 | 74.23 ±1.170 · 10−14 | 0.816
DOM Similarity | 95.35 ±1.242 · 10−2 | 3.732 ±1.866 · 10−3 | 59.28 ±8.929 · 10−3 | 0.995
