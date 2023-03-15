static void main(String[] args) {
    def a=[
            java:{
                println("aaa")
            }
    ]
    a.get("java").call()
}