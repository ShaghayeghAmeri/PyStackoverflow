from types import SimpleNamespace

from src.utils.keyboard import create_keyboard
import emoji

keys = SimpleNamespace(
    settings=':gear: Settings',
    cancel=':cross_mark: Cancel',
    back=':arrow_left: Back',
    next=':arrow_right: Next',
    add=':heavy_plus_sign: Add',
    save=':check_mark_button: Save',
    yes=':white_check_mark: Yes',
    no=':negative_squared_cross_mark: No',
    ask_question=':red_question_mark: Ask a Question',
    send_post=':envelope_with_arrow: Send',
    send_answer=':envelope_with_arrow: Send Answer',
    send_quastion=':light_bulb: Send Question'
)

keyboards = SimpleNamespace(
    main=create_keyboard(keys.ask_question, keys.settings),
    ask_quastion=create_keyboard(keys.cancel, keys.send_quastion)
)

states = SimpleNamespace(
    main='MAIN',
    ask_question='ASK_QUASTION',
)
