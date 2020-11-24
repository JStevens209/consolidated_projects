#pragma once
// leak detection using the C Run-Time (CRT) Library
// setup simplified by K. Shomper for CS1220
//   -- to have line numbers reported replace allocations which use new 
//      with NEW
// documentation at https://docs.microsoft.com/en-us/visualstudio/debugger/finding-memory-leaks-using-the-crt-library?view=vs-2019
#ifdef _DEBUG
   #include <cstdlib>
   #include <crtdbg.h>
   #define _CRTDBG_MAP_ALLOC

   #define NEW new ( _NORMAL_BLOCK , __FILE__ , __LINE__ )
   static void init_leak_check() {
      _CrtSetDbgFlag ( _CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF );
   }

   static class LeakCheck {
     public:
       LeakCheck() { init_leak_check(); }
   } lc;
#else
    #define NEW new
#endif
