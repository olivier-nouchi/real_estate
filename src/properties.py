import logging
from utils import load_properties_info

logger = logging.getLogger(f"{__name__}")

class Property:
    id: str




    @staticmethod
    def load_properties() -> dict:
        """

        :return:
        """
        return load_properties_info()

    @staticmethod
    def count_unique_properties(properties: dict) -> int:
        """

        :return:
        """
        return len(set(properties))

    @staticmethod
    def count_properties(properties: dict) -> int:
        """

        :return:
        """
        return len(properties)


def main():
    n_unique_properties = Property().count_unique_properties(properties=load_properties_info())
    n_properties = Property().count_properties(properties=load_properties_info())
    logger.info(n_unique_properties)
    logger.info(n_properties)


if __name__ == '__main__':
    main()
