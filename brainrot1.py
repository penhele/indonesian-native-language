def skibidi_interpreter():
    print("🚀 Welcome to SkibidiLang 💀")
    print("Commands:")
    print("- GYAT <teks>  → print teks")
    print("- RIZZ <angka1> <angka2> → tambah angka (no cap math)")
    print("- SKIBIDI → keluar (because ur cooked)\n")

    while True:
        user_input = input("🧠 > ").strip()
        if not user_input:
            continue

        parts = user_input.split()
        cmd = parts[0].upper()

        if cmd == "GYAT":
            print("💬", " ".join(parts[1:]), "🔥")

        elif cmd == "RIZZ":
            try:
                a = float(parts[1])
                b = float(parts[2])
                print(f"🧮 Result: {a + b} (sigma move 💪)")
            except (IndexError, ValueError):
                print("⚠️ Bro… that ain't valid input 💀 (pakai: RIZZ <angka1> <angka2>)")

        elif cmd == "SKIBIDI":
            print("💀💀 You just left SkibidiLang. Go touch grass 🌱")
            break

        else:
            print("❓ Bro what is that command?? Try again 💀")


# Jalankan interpreter
skibidi_interpreter()
