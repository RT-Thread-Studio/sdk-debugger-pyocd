import os


with open("../pyocd.yaml", mode='w') as f:
    f.write("""
pack:
""")
    for file in os.listdir():
        if str(file).endswith(".pack"):
            f.write("  - ./packs/"+str(file)+"\n")
