#include <iostream>

#include "myexceptions.h"

void foo(){
    TRY(
        THROW(Exception_A)
    )
    CATCH(Exception_B,
        std::cout << "Exception_B" << std::endl;
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