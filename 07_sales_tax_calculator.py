#Sales Tax Calculator
total_sales = 0
sales_employees = 5

for i in range(sales_employees):
    sales_amount = float(input(f"Enter the daily sales amount for employee {i + 1} (in Rs.): "))
    
    if sales_amount < 50000:
        tax_rate = 0.05
    elif sales_amount <= 100000:
        tax_rate = 0.10
    else:
        tax_rate = 0.15

    tax_amount = sales_amount * tax_rate
    total_sales += sales_amount

    print(f"Employee {i + 1}:")
    print(f"  Sales Amount: Rs. {sales_amount:.2f}")
    print(f"  Tax Amount: Rs. {tax_amount:.2f}")

average_sales = total_sales / sales_employees

print("\nSummary:")
print(f"Total Sales: Rs. {total_sales: .2f}")
print(f"Average Sales: Rs. {average_sales: .2f}")