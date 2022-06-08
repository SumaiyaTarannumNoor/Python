#Taking kilometers input from the user

n = Kilometers = Miles = float(input("Enter the distance: "))
print("\n1 Kilometer = 0.621371 Miles.\n")

print("1. Kilometers to Miles conversion.")
print("2. Miles to Kilometers conversion.")
choice = int (input("\nEnter your conversion choice: \n"))


#conversion factor
conv_fac = 0.621371

#calculate miles
if choice==1:
    Miles = Kilometers * conv_fac
    print('%0.2f kilometers is equal to %0.2f miles.' %(Kilometers, Miles))

if choice==2:
    Kilometers = Miles / conv_fac
    print('%0.2f Miles is equal to %0.2f Kilometers.' %(Miles, Kilometers))
