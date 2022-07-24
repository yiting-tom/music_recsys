# The Music RecSys Scrapy System

## data folder
- all data is stored in the data folder
- the data folder structure should be as follows:
  ```sh
  data
  ├── <spider-a-name>
  │   ├── htm
  │   │    ├── ...
  │   │    └── foo.htm
  │   └── pkl (optional)
  │        ├── ...
  │        └── bar.pkl
  ...
  └── <spider-n-name>
      ├── htm
      │    ├── ...
      │    └── foo.htm
      └── pkl (optional)
           ├── ...
           └── bar.pkl
  ```


## spiders module
- All spiders are located in the `spiders` directory.
- The output file format of `spiders` should be *html* or *htm*
