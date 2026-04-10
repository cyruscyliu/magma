<?php

#[\Deprecated]
const DeprecatedConst1 = 1;

#[\Deprecated("use DEPRECATED_CONST_2")]
const DeprecatedConst2 = 2;

#[\Deprecated(message: "use DEPRECATED_CONST_3")]
const DeprecatedConst3 = 3;

#[\Deprecated(message: "use DEPRECATED_CONST_4", since: "1.0")]
const DeprecatedConst4 = 4;

#[\Deprecated("use DEPRECATED_CONST_5", "1.0")]
const DeprecatedConst5 = 5;

#[\Deprecated(since: "1.0")]
const DeprecatedConst6 = 6;

echo DeprecatedConst1 . "\n";
echo DeprecatedConst2 . "\n";
echo DeprecatedConst3 . "\n";
echo DeprecatedConst4 . "\n";
echo DeprecatedConst5 . "\n";
echo DeprecatedConst6 . "\n";
?>