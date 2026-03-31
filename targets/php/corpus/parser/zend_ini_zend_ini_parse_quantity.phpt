<?php

// This test checks valid formats do not throw any warnings.
foreach (['', ' '] as $leadingWS) {
  foreach (['', '+', '-'] as $sign) {
    foreach (['', ' '] as $midWS) {
      foreach (['', 'K', 'k', 'M', 'm', 'G', 'g'] as $exp) {
        foreach (['', ' '] as $trailingWS) {
          // Decimal
          $setting = sprintf('%s%s1%s%s%s',
                             $leadingWS, $sign, $midWS, $exp, $trailingWS);
          printf("# \"%s\"\n", $setting);
          var_dump(zend_test_zend_ini_parse_quantity($setting));
          print "\n";

          if ($exp !== 'g' && $exp !== 'G') { // Would overflow
              // Octal
              $setting = sprintf('%s%s0123%s%s%s',
                                 $leadingWS, $sign, $midWS, $exp, $trailingWS);
              printf("# \"%s\"\n", $setting);
              var_dump(zend_test_zend_ini_parse_quantity($setting));
              print "\n";
          }
        }
      }
    }
  }
}