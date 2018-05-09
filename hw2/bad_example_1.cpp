#include <iostream>

#include "myexceptions.h"

class GoodInt : public SafeClass {
public:
    GoodInt(int a) : value(a) {}

    virtual ~GoodInt() {
        std::cout << "destruct " << value << std::endl;
    }

    int value;
};

class BadInt : public SafeClass {
public:
    BadInt(int a) : value(a) {}

    virtual ~BadInt() {
        std::cout << "destruct " << value << std::endl;
        THROW(Exception_D);
    }

    int value;
};

int main() {
    TRY(
            GoodInt b = {4};
            THROW(Exception_A)
    )
            CATCH(Exception_A,
                  std::cout << "Exception_A" << std::endl;
            )
            CATCH(Exception_B,
                  std::cout << "Exception_B" << std::endl;
            )
    ENDTRY

    TRY(
            BadInt b = {5};
            THROW(Exception_B)
    )
            CATCH(Exception_A,
                  std::cout << "Exception_A" << std::endl;
            )
            CATCH(Exception_B,
                  std::cout << "Exception_B" << std::endl;
            )
    ENDTRY
}