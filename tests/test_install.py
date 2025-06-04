import logomaker_batch

def main():
    print("logomaker_batch loaded successfully.")
    print("Available submodules or attributes:")
    for attr in dir(logomaker_batch):
        if not attr.startswith("_"):
            print(f"  - {attr}")

if __name__ == "__main__":
    main()
