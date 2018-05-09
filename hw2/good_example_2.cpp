#include <iostream>

#include "myexceptions.h"

void boo() {
    THROW(Exception_B);
}

void coo() {
    THROW(Exception_C);
}

void foo() {
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
        foo();
    )
    CATCH(Exception_C,
        std::cout << "Exception_C" << std::endl;
    )
    ENDTRY
}