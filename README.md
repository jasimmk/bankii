# Bankii
Open Bank statement parser. Converts multiple bank statements to a single csv format, which you can import in Googlesheets/Excel, to manage. Please check supported banks if your bank is supported. If not you can check Contribution section to add your bank.

## Basic setup

### Save files with specific format in a folder
You need to download bank statements from your bank. And keep it the filenames in specific format. Currently parsers supported is xls and csv for certain banks. You can check `bankii/banks` folder for supported banks.

### Filenames:
```
<8LetterSWIFT>__<3lettercurrency>__<accountno>__<fileidentification>.csv
<8LetterSWIFT>__<3lettercurrency>__<accountno>__<fileidentification>.xls
```
- 8LetterSWIFT: `Mandatory`: Extract first 8 digits of bank swift code Eg: `SBININBB` for `State Bank of India`. Check supported bank list below
- 3lettercurrency: `Mandatory`: Currency code. Eg: `INR` for `Indian Rupee`
- accountno: Account number. Eg: `20140000000` State bank of India account number. This data is copied at the account number field in the report.
- fileidentification: Its generally advised to add statement dates with account prefixes. `ONR01012019-30062019`, Just to mean statement its an ONR account statement from 1st January 2019 to 30th June 2019. This is a free text column though.

### Eg: values
```
SBININBB__INR__20140000009__SBI01012019-30062019
MEBLAEAD__AED__3700000000001__CURRENT01012019-17052020.xls
KKBKINBB__INR__4410000001__KOTAK01102019-31122019.csv
```

## Installation
Requires python 3.7 or above
```
pip install -r requirements.txt
```
### Running the app

```
$ python app.py -s /Users/user/bank/statements/ -d /Users/user/bank/clean
```

### Output
By default at folder `/Users/user/bank/clean/output.csv` you will get a clean statement containing all your banks records.

## Contributing

Please create an issue and explain the problem, and your approach to solve it, and raise a Merge request.
### Adding a new bank
- Please check `bankii/banks` and copy the py file, and use similiar format for your bank.

## Supported banks


| Bank                  | Country | Swift    | Steps                                                                                           |
|-----------------------|---------|----------|-------------------------------------------------------------------------------------------------|
| Federal Bank          | IN      | FDRLINBB | Download the statement file in xls format                                                       |
| State Bank of India   | IN      | SBININBB | Download the statement file in csv format                                                       |
| Kotak Bank            | IN      | KKBKINBB | Download the statement file in csv format                                                       |
| Emirates Islamic Bank | AE      | MEBLAEAD | Download the statement file in excel format. Open it on excel and save again as Excel 97 format |
