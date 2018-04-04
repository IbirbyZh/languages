#include <iostream>

#include "myexceptions.h"

class Int : public SafeClass {
public:
    explicit Int(int a) : value(a) {}

    virtual void Destruct() override {
        std::cerr << "destruct " << value << std::endl;
        SafeClass::Destruct();
    }

    virtual ~Int() {
        Destruct();
    }

    int value;
};

void foo(Int a) {
    Int b = {1000};
    if (a.value > 9) {
        THROW(Exception_A);
    } else {
        std::cout << a.value << std::endl;
    }
}

void boo() {
    THROW(Exception_B);
}

void coo() {
    THROW(Exception_C);
}

void foo(){
    TRY(
        boo();
    )
    CATCH(Exception_B,
        std::cout << "Exception_B in foo" << std::endl;
    )
    ENDTRY

    TRY(
        coo();
    )
    CATCH(Exception_B,
        std::cout << "Exception_B in foo" << std::endl;
    )
    ENDTRY
}

int main() {
    TRY(
            foo({1});
            foo({4});
            foo({10});
    )
    CATCH(Exception_A,
          std::cout << "Exception_A" << std::endl;
    )
    CATCH(Exception_B,
          std::cout << "Exception_B" << std::endl;
    )
    ENDTRY
    TRY(
        foo();
    )
    CATCH(Exception_C,
          std::cout << "Exception_C" << std::endl;
    )
    ENDTRY
}