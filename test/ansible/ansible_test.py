import ansible.cli.playbook

if __name__ == '__main__':
    a1 = {
        "a": "1",
        "a1": {
            "a11": "haha"
        },
        "a2": ["1", "2"]
    }
    b1 = {
        "a": "2",
        "a1": {
            "a11": "hoho"
        },
        "a2": ["3", "4", "5", "6"]
    }
    c = vars.combine_vars(
        a1, b1
    )
    ansible.cli.playbook.PlaybookCLI(args={}).run()
    print("a")
