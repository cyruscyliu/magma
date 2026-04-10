<?php

// This test checks valid formats do not throw any warnings.
foreach (['', ' '] as $leadingWS) {
  foreach (['', '+', '-'] as $sign) {
    foreach (['', ' '] as $midWS) {
      // Ignore G due to overflow on 32bits
      foreach (['', 'K', 'k', 'M', 'm'] as $exp) {
        foreach (['', ' '] as $trailingWS) {
          $setting = sprintf('%s%s0o14%s%s%s',
                             $leadingWS, $sign, $midWS, $exp, $trailingWS);
          printf("# \"%s\"\n", $setting);
          var_dump(zend_test_zend_ini_parse_quantity($setting));
          print "\n";

          $setting = sprintf('%s%s0O14%s%s%s',
                             $leadingWS, $sign, $midWS, $exp, $trailingWS);
          printf("# \"%s\"\n", $setting);
          var_dump(zend_test_zend_ini_parse_quantity($setting));
          print "\n";
        }
      }
    }
  }
}
?>