#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_basic_drills.py
#  kanji_test
# 
#  Created by Lars Yencken on 26-11-2008.
#  Copyright 2008 Lars Yencken. All rights reserved.
#

import unittest

from django.contrib.auth.models import User

from kanji_test.user_model.models import PartialLexeme, Syllabus, ErrorDist
from kanji_test.plugins import basic_drills

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(SurfaceQuestionTest),
        ))
    return testSuite

class SurfaceQuestionTest(unittest.TestCase):
    def setUp(self):
        User.objects.filter(username='test_user').delete()
        test_user = User(username='test_user')
        test_user.save()
        self.syllabus = Syllabus.objects.get(tag='jlpt 4')
        test_user.userprofile_set.create(syllabus=self.syllabus)
        ErrorDist.init_from_priors(test_user)
        self.user = test_user

        self.factory = basic_drills.SurfaceQuestionFactory()

    def test_bug_325(self):
        partial_lexeme = PartialLexeme.objects.get(
                syllabus=self.syllabus,
                surface_set__surface=u'九つ',
                reading_set__reading=u'ここのつ',
            )
        
        # [325] an infinite loop here
        question = self.factory.get_question(partial_lexeme, self.user)

        # If we get here, it worked.
        question.options.all().delete()
        question.delete()
    
    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:
