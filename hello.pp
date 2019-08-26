func hello(name=null) {
    if (name == null) {
        name = 'World'
    }
    print('Hello', name)
}

func main() {
    hello()
    hello("Python Plus Plus")
}

main()
