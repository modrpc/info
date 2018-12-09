import lib

def main():
        nyse = lib.Market("NYSE", "../data/nyse.csv")
        nasdaq = lib.Market("NASDAQ", "../data/nasdaq.csv")

if __name__ == '__main__':
    main()

