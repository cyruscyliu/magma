<?php

#[\Deprecated(TEST)]
const TEST = "from itself";

#[\Deprecated]
const TEST2 = "from another";

#[\Deprecated(TEST2)]
const TEST3 = 1;

TEST;
TEST3;

?>