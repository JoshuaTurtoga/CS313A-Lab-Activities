import os


def clear_console():
    os.system('cls')


def is_sorted(arr):

    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


def main():
    while True:
        clear_console()
        print("    =========================")
        print("   |  Array Sort Validator  |")
        print("    =========================\n")

        try:
            input_str = input("\nEnter numbers separated by spaces: ")
            arr = [int(x) for x in input_str.split()]

            if not arr:
                print("Please enter at least one number.")
                continue

            print("\nOriginal array:", arr)

            if is_sorted(arr):
                print("Remark: The array is already sorted!")
            else:
                sorted_arr = sorted(arr)
                print("Remark: The array is not sorted.")
                print("Sorted array:", sorted_arr)

        except ValueError:
            print("Invalid input! Please enter valid numbers separated by spaces.")
            continue

        while True:
            try_again = input("\nDo you want to try again? (yes/no): ").lower()
            if try_again in ['yes', 'y', 'no', 'n']:
                break
            print("Please enter 'yes' or 'no'")

        if try_again not in ['yes', 'y']:
            clear_console()
            print("    =========================")
            print("   |  Array Sort Validator   |")
            print("    =========================\n")
            print("Thank you for using the program!")
            break


if __name__ == "__main__":
    main()
