#!/bin/bash


while :
do

ADB=$(adb devices)

if [ $? -eq 0 ]
then
  
  
  
package=$(adb shell dumpsys window windows | grep -E 'mFocusedApp'| cut -d / -f 1 | cut -d " " -f 6)
  while [[ $package != "com.android.launcher" ]]
  do
  echo $?
  
  echo $package
  getprocessid=$(adb shell ps | grep $package | head -n 1 | awk -F ' ' '{print $2}')
  fname=$(adb shell ls /data/local/tmp/ | awk '{printf("%s",$0);exit}')
  echo $fname
  echo $getprocessid
  adb shell strace -t -f -p $getprocessid >> ~/$fname
  package=$(adb shell dumpsys window windows | grep -E 'mFocusedApp'| cut -d / -f 1 | cut -d " " -f 6)
  done


  echo $package
  
fi

done





