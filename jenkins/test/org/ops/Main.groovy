static void main(String[] args) {
//    def a = [
//            java: {
//
//            }
//    ]
//    a.get("java").call()

    Map<String, Object> a = new HashMap<>();
    a.put("a", "111");
    a.put("b", "null")
    a.put("c", "null")
    def b = a.findAll { k, v -> v in String && v == "null" }.each {
        it.value = null
        return it
    }
    println "aa"
}