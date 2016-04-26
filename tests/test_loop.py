# encoding: utf-8
# Copyright (C) 2015 John Törnblom

from utils import RSLTestCase
from utils import evaluate_docstring


class TestLoop(RSLTestCase):

    @evaluate_docstring
    def test_while_loop(self, rc):
        '''
        .assign x = 10
        .while (x > 0)
            .assign x = x - 1
        .end while
        .exit x
        '''
        self.assertEqual(0, rc)
        
    @evaluate_docstring
    def test_while_loop_break(self, rc):
        '''
        .assign x = 10
        .while (x > 0)
            .if (x == 5)
                .break while
            .end if
            .assign x = x - 1
        .end while
        .exit x
        '''
        self.assertEqual(5, rc)
        
    def test_for_loop(self):
        self.metamodel.define_class('A', [])

        text = '''
        .select many a_set from instances of A
        .assign x = 0
        .for each a in a_set
            .assign x = x + 1
        .end for
        .exit x
        '''
        
        for i in range(0, 10):
            rc = self.eval_text(text)
            self.assertEqual(i, rc)
            self.metamodel.new('A')
        
    def test_for_loop_break(self):
        self.metamodel.define_class('A', [])

        text = '''
        .select many a_set from instances of A
        .assign x = 0
        .for each a in a_set
            .if (x == 3)
                .break for
            .end if
            .assign x = x + 1
        .end for
        .exit x
        '''

        for _ in range(0, 10):
            self.metamodel.new('A')
            
        rc = self.eval_text(text)
        self.assertEqual(3, rc)

    def test_first_in_loop(self):
        self.metamodel.define_class('A', [('ID', 'integer')])

        text = '''
        .select many a_set from instances of A
        .assign x = 0
        .for each a in a_set
            .if (first a_set)
                .assign x = a.ID + x
            .end if
        .end for
        .exit x
        '''
        
        self.metamodel.new('A', ID=42);
        self.metamodel.new('A', ID=1);
        self.metamodel.new('A', ID=1);
        self.metamodel.new('A', ID=1);
        self.metamodel.new('A', ID=1);
        self.metamodel.new('A', ID=1);
        self.metamodel.new('A', ID=1);
        self.metamodel.new('A', ID=1);
        self.metamodel.new('A', ID=1);
        self.metamodel.new('A', ID=1);
            
        rc = self.eval_text(text)
        self.assertEqual(42, rc)

    def test_not_first_in_loop(self):
        self.metamodel.define_class('A', [('ID', 'integer')])

        text = '''
        .select many a_set from instances of A
        .assign x = 0
        .for each a in a_set
            .if (not_first a_set)
                .assign x = a.ID + x
            .end if
        .end for
        .exit x
        '''
        
        self.metamodel.new('A', ID=42);
        self.metamodel.new('A', ID=0);
        self.metamodel.new('A', ID=0);
        self.metamodel.new('A', ID=0);
        self.metamodel.new('A', ID=0);
        self.metamodel.new('A', ID=0);
        self.metamodel.new('A', ID=0);
        self.metamodel.new('A', ID=0);
        self.metamodel.new('A', ID=0);
        self.metamodel.new('A', ID=0);
            
        rc = self.eval_text(text)
        self.assertEqual(0, rc)
        
    def test_last_in_loop(self):
        self.metamodel.define_class('A', [('ID', 'integer')])

        text = '''
        .select many a_set from instances of A
        .assign x = 0
        .for each a in a_set
            .if (last a_set)
                .assign x = a.ID + x
            .end if
        .end for
        .exit x
        '''
        
        self.metamodel.new('A', ID=1);
        self.metamodel.new('A', ID=1);
        self.metamodel.new('A', ID=1);
        self.metamodel.new('A', ID=1);
        self.metamodel.new('A', ID=1);
        self.metamodel.new('A', ID=1);
        self.metamodel.new('A', ID=1);
        self.metamodel.new('A', ID=1);
        self.metamodel.new('A', ID=1);
        self.metamodel.new('A', ID=42);
            
        rc = self.eval_text(text)
        self.assertEqual(42, rc)
        
    def test_not_last_in_loop(self):
        self.metamodel.define_class('A', [('ID', 'integer')])

        text = '''
        .select many a_set from instances of A
        .assign x = 0
        .for each a in a_set
            .if (not_last a_set)
                .assign x = a.ID + x
            .end if
        .end for
        .exit x
        '''
        
        self.metamodel.new('A', ID=0);
        self.metamodel.new('A', ID=0);
        self.metamodel.new('A', ID=0);
        self.metamodel.new('A', ID=0);
        self.metamodel.new('A', ID=0);
        self.metamodel.new('A', ID=0);
        self.metamodel.new('A', ID=0);
        self.metamodel.new('A', ID=0);
        self.metamodel.new('A', ID=0);
        self.metamodel.new('A', ID=42);
            
        rc = self.eval_text(text)
        self.assertEqual(0, rc)
        
