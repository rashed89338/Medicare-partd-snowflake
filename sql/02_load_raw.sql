-- 02_load_raw.sql
-- Preserve original source values as VARCHAR. Stage upload must be completed
-- separately in Snowsight (Add Data -> Load files into a Stage).
USE ROLE PARTD_ANALYST;
USE WAREHOUSE PARTD_WH;
USE SCHEMA MEDICARE_PARTD.RAW;

CREATE TABLE IF NOT EXISTS RAW.SPENDING_BY_DRUG (
    BRND_NAME                             VARCHAR,
    GNRC_NAME                             VARCHAR,
    TOT_MFTR                              VARCHAR,
    MFTR_NAME                             VARCHAR,
    TOT_SPNDNG_2020                       VARCHAR,
    TOT_DSG_UNTS_2020                     VARCHAR,
    TOT_CLMS_2020                         VARCHAR,
    TOT_BENES_2020                        VARCHAR,
    AVG_SPND_PER_DSG_UNT_WGHTD_2020       VARCHAR,
    AVG_SPND_PER_CLM_2020                 VARCHAR,
    AVG_SPND_PER_BENE_2020                VARCHAR,
    OUTLIER_FLAG_2020                     VARCHAR,
    TOT_SPNDNG_2021                       VARCHAR,
    TOT_DSG_UNTS_2021                     VARCHAR,
    TOT_CLMS_2021                         VARCHAR,
    TOT_BENES_2021                        VARCHAR,
    AVG_SPND_PER_DSG_UNT_WGHTD_2021       VARCHAR,
    AVG_SPND_PER_CLM_2021                 VARCHAR,
    AVG_SPND_PER_BENE_2021                VARCHAR,
    OUTLIER_FLAG_2021                     VARCHAR,
    TOT_SPNDNG_2022                       VARCHAR,
    TOT_DSG_UNTS_2022                     VARCHAR,
    TOT_CLMS_2022                         VARCHAR,
    TOT_BENES_2022                        VARCHAR,
    AVG_SPND_PER_DSG_UNT_WGHTD_2022       VARCHAR,
    AVG_SPND_PER_CLM_2022                 VARCHAR,
    AVG_SPND_PER_BENE_2022                VARCHAR,
    OUTLIER_FLAG_2022                     VARCHAR,
    TOT_SPNDNG_2023                       VARCHAR,
    TOT_DSG_UNTS_2023                     VARCHAR,
    TOT_CLMS_2023                         VARCHAR,
    TOT_BENES_2023                        VARCHAR,
    AVG_SPND_PER_DSG_UNT_WGHTD_2023       VARCHAR,
    AVG_SPND_PER_CLM_2023                 VARCHAR,
    AVG_SPND_PER_BENE_2023                VARCHAR,
    OUTLIER_FLAG_2023                     VARCHAR,
    TOT_SPNDNG_2024                       VARCHAR,
    TOT_DSG_UNTS_2024                     VARCHAR,
    TOT_CLMS_2024                         VARCHAR,
    TOT_BENES_2024                        VARCHAR,
    AVG_SPND_PER_DSG_UNT_WGHTD_2024       VARCHAR,
    AVG_SPND_PER_CLM_2024                 VARCHAR,
    AVG_SPND_PER_BENE_2024                VARCHAR,
    OUTLIER_FLAG_2024                     VARCHAR,
    CHG_AVG_SPND_PER_DSG_UNT_23_24        VARCHAR,
    CAGR_AVG_SPND_PER_DSG_UNT_20_24       VARCHAR,
    _LOADED_AT TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    _SOURCE_FILE VARCHAR
);

-- Preview staged files using: LIST @RAW.CMS_STAGE;
COPY INTO RAW.SPENDING_BY_DRUG (
    BRND_NAME,
    GNRC_NAME,
    TOT_MFTR,
    MFTR_NAME,
    TOT_SPNDNG_2020,
    TOT_DSG_UNTS_2020,
    TOT_CLMS_2020,
    TOT_BENES_2020,
    AVG_SPND_PER_DSG_UNT_WGHTD_2020,
    AVG_SPND_PER_CLM_2020,
    AVG_SPND_PER_BENE_2020,
    OUTLIER_FLAG_2020,
    TOT_SPNDNG_2021,
    TOT_DSG_UNTS_2021,
    TOT_CLMS_2021,
    TOT_BENES_2021,
    AVG_SPND_PER_DSG_UNT_WGHTD_2021,
    AVG_SPND_PER_CLM_2021,
    AVG_SPND_PER_BENE_2021,
    OUTLIER_FLAG_2021,
    TOT_SPNDNG_2022,
    TOT_DSG_UNTS_2022,
    TOT_CLMS_2022,
    TOT_BENES_2022,
    AVG_SPND_PER_DSG_UNT_WGHTD_2022,
    AVG_SPND_PER_CLM_2022,
    AVG_SPND_PER_BENE_2022,
    OUTLIER_FLAG_2022,
    TOT_SPNDNG_2023,
    TOT_DSG_UNTS_2023,
    TOT_CLMS_2023,
    TOT_BENES_2023,
    AVG_SPND_PER_DSG_UNT_WGHTD_2023,
    AVG_SPND_PER_CLM_2023,
    AVG_SPND_PER_BENE_2023,
    OUTLIER_FLAG_2023,
    TOT_SPNDNG_2024,
    TOT_DSG_UNTS_2024,
    TOT_CLMS_2024,
    TOT_BENES_2024,
    AVG_SPND_PER_DSG_UNT_WGHTD_2024,
    AVG_SPND_PER_CLM_2024,
    AVG_SPND_PER_BENE_2024,
    OUTLIER_FLAG_2024,
    CHG_AVG_SPND_PER_DSG_UNT_23_24,
    CAGR_AVG_SPND_PER_DSG_UNT_20_24,
    _SOURCE_FILE
)
FROM (
    SELECT t.$1, t.$2, t.$3, t.$4, t.$5, t.$6, t.$7, t.$8, t.$9, t.$10, t.$11, t.$12, t.$13, t.$14, t.$15, t.$16, t.$17, t.$18, t.$19, t.$20, t.$21, t.$22, t.$23, t.$24, t.$25, t.$26, t.$27, t.$28, t.$29, t.$30, t.$31, t.$32, t.$33, t.$34, t.$35, t.$36, t.$37, t.$38, t.$39, t.$40, t.$41, t.$42, t.$43, t.$44, t.$45, t.$46, METADATA$FILENAME
    FROM @RAW.CMS_STAGE t
)
FILE_FORMAT = (FORMAT_NAME = 'RAW.CSV_FMT')
ON_ERROR = 'ABORT_STATEMENT';

SELECT COUNT(*) AS TOTAL_ROWS,
       COUNT_IF(MFTR_NAME = 'Overall') AS DRUG_LEVEL_ROWS
FROM RAW.SPENDING_BY_DRUG;
