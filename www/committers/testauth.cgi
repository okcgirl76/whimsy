#!/usr/bin/env ruby
PAGETITLE = "Board Agenda Auth Tester" # Wvisible:board tools
#
# Small CGI to help debug board agenda authentication issues
#

$LOAD_PATH.unshift File.realpath(File.expand_path('../../../lib', __FILE__))
require 'wunderbar'
require 'wunderbar/bootstrap'
require 'whimsy/asf/rack'
require 'whimsy/asf/agenda'

_html do
  _whimsy_body(
    title: PAGETITLE,
    related: {
      '/board/minutes/' => 'Board Meeting Minutes (public)',
      '/board/agenda/' => 'Board Agenda Tool (restricted)',
      '/status/' => 'Whimsy Server Status'
    },
    helpblock: -> {
      _ 'This script checks your authorization to use the agenda tool, and checks if you are listed as attending the current board meeting in the official agenda.'
    }
  ) do
    FOUNDATION_BOARD = ASF::SVN['foundation_board']
    agenda = Dir[File.join(FOUNDATION_BOARD, 'board_agenda_*.txt')].sort.last.untaint
    agenda = ASF::Board::Agenda.parse(File.read(agenda))
    roll = agenda.find {|item| item['title'] == 'Roll Call'}

    person = ASF::Auth.decode(env)
    _table do
      _tr do
        _td 'User id'
        _td person.id
      end

      _tr do
        _td 'ASF Member?'
        _td person.asf_member?
      end

      _tr do
        _td 'PMC chair?'
        _td ASF.pmc_chairs.include? person
      end

      _tr do
        _td 'Attending'
        _td roll['people'].keys.include? person.id
      end
    end
  end
end
