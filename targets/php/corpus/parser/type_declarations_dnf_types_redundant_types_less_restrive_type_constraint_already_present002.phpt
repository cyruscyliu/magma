<?php

interface A {}
interface B {}

function test(): A|(A&B) {}

?>
===DONE===