#pragma once

#include <iostream>
#include <csetjmp>
#include <set>

struct SafeClass;


namespace {
    const int MAX_DEPTH = 128;
    std::jmp_buf env[MAX_DEPTH];
    std::set<SafeClass *> objects[MAX_DEPTH];
    int currentEnv = -1;
    bool inClearStack = false;
}

#define TRY(statements) {\
    ++currentEnv; \
    objects[currentEnv].clear(); \
    int exceptionFlag = setjmp(env[currentEnv]); \
    switch (exceptionFlag) { \
        case 0: \
        {statements} \
        break;

#define ENDTRY \
        default: \
        --currentEnv; \
        if (currentEnv < 0) {std::cerr << "unhandled exception" << std::endl; exit(1);} \
        std::longjmp(env[currentEnv], exceptionFlag); \
        break; \
    } \
    --currentEnv; \
}

#define CATCH(exception_flag, statements) \
    case exception_flag: \
    {statements} \
    break;

void clearStack();

#define THROW(exception_flag) { \
    clearStack(); \
    std::longjmp(env[currentEnv], exception_flag); \
}

enum TException {
    Exception_A = 1,
    Exception_B = 2,
    Exception_C = 3,
    Exception_D = 4
};

struct SafeClass {
    SafeClass() {
        objects[currentEnv].insert(this);
    }

    virtual void Destruct() {
        if (!inClearStack) {
            objects[currentEnv].erase(this);
        }
    }

    virtual ~SafeClass(){
        Destruct();
    }
};

void clearStack() {
    std::cerr << "start clear stack" << std::endl;
    inClearStack = true;
    for (SafeClass *a:objects[currentEnv]) {
        a->Destruct();
    }
    inClearStack = false;
    std::cerr << "end clear stack" << std::endl;
}