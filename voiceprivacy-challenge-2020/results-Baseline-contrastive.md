| System               | Gender   | Dataset     | Task   |   ROCCH-EER [%] |   ZEBRA Population [bit] |   ZEBRA Individual | ZEBRA Category   |   Cllr |   min Cllr |
|:---------------------|:---------|:------------|:-------|----------------:|-------------------------:|-------------------:|:-----------------|-------:|-----------:|
| Baseline-contrastive | f        | libri       | a-a    |           15    |                    0.358 |              3.577 | C                |  12.54 |       0.49 |
| Baseline-contrastive | f        | libri       | o-a    |           25.57 |                    0.219 |              2.236 | C                | 115.57 |       0.69 |
| Baseline-contrastive | f        | libri       | o-o    |            7.18 |                    0.584 |              3.976 | C                |  26.81 |       0.18 |
| Baseline-contrastive | f        | vctk        | a-a    |           16.89 |                    0.315 |              2.626 | C                |  41.34 |       0.55 |
| Baseline-contrastive | f        | vctk        | o-a    |           29.9  |                    0.141 |              2.407 | C                |  93.16 |       0.79 |
| Baseline-contrastive | f        | vctk        | o-o    |            4.86 |                    0.594 |              3.66  | C                |   1.49 |       0.17 |
| Baseline-contrastive | f        | vctk_common | a-a    |           14.07 |                    0.377 |              2.225 | C                |  42.75 |       0.46 |
| Baseline-contrastive | f        | vctk_common | o-a    |           30.45 |                    0.132 |              1.213 | B                |  93.96 |       0.81 |
| Baseline-contrastive | f        | vctk_common | o-o    |            2.75 |                    0.652 |              3.557 | C                |   0.86 |       0.09 |
| Baseline-contrastive | m        | libri       | a-a    |            8.24 |                    0.525 |              3.536 | C                |  15.39 |       0.26 |
| Baseline-contrastive | m        | libri       | o-a    |           17.53 |                    0.355 |              2.602 | C                | 106.44 |       0.5  |
| Baseline-contrastive | m        | libri       | o-o    |            1.07 |                    0.69  |              3.924 | C                |  15.34 |       0.04 |
| Baseline-contrastive | m        | vctk        | a-a    |           11.93 |                    0.425 |              3.516 | C                |  25.07 |       0.4  |
| Baseline-contrastive | m        | vctk        | o-a    |           27.99 |                    0.196 |              3.009 | C                | 101.7  |       0.72 |
| Baseline-contrastive | m        | vctk        | o-o    |            1.97 |                    0.667 |              3.921 | C                |   1.82 |       0.07 |
| Baseline-contrastive | m        | vctk_common | a-a    |           11.22 |                    0.463 |              3.09  | C                |  28.23 |       0.35 |
| Baseline-contrastive | m        | vctk_common | o-a    |           23.99 |                    0.198 |              2.468 | C                |  99.34 |       0.71 |
| Baseline-contrastive | m        | vctk_common | o-o    |            0.97 |                    0.694 |              3.675 | C                |   1.04 |       0.04 |