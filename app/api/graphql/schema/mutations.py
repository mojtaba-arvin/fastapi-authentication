"""
GraphQL schema definitions for mutations related to user authentication and management.
"""
from ariadne import make_executable_schema, gql
from app.api.graphql.resolvers.user_resolvers import mutation

# Define GraphQL schema using SDL (Schema Definition Language)
type_defs = gql("""
    type Query {
        _empty: String
    }

    type LoginResponse {
        access_token: String!
        token_type: String!
        refresh_token: String
        id_token: String
    }

    type SignUpResponse {
        message: String!
        user_sub: String
    }

    type ConfirmSignUpResponse {
        message: String!
    }

    type ResendConfirmationCodeResponse {
        message: String!
    }

    type TokenRefreshResponse {
        access_token: String!
        token_type: String!
        id_token: String
    }

    type ChangePasswordResponse {
        message: String!
    }

    type ForgotPasswordResponse {
        message: String!
    }

    type ConfirmForgotPasswordResponse {
        message: String!
    }

    type UpdateUserAttributesResponse {
        message: String!
    }

    type Mutation {
        login(username: String!, password: String!): LoginResponse!
        signUp(username: String!, password: String!, email: String!, phone_number: String, given_name: String, family_name: String): SignUpResponse!
        confirmSignUp(username: String!, confirmation_code: String!): ConfirmSignUpResponse!
        resendConfirmationCode(username: String!): ResendConfirmationCodeResponse!
        refreshToken(refresh_token: String!): TokenRefreshResponse!
        changePassword(access_token: String!, previous_password: String!, proposed_password: String!): ChangePasswordResponse!
        forgotPassword(username: String!): ForgotPasswordResponse!
        confirmForgotPassword(username: String!, confirmation_code: String!, new_password: String!): ConfirmForgotPasswordResponse!
        updateUserAttributes(access_token: String!, attributes: [AttributeInput]!): UpdateUserAttributesResponse!
    }

    input AttributeInput {
        name: String!
        value: String!
    }
""")

# Create the executable schema by combining type definitions and resolvers
schema = make_executable_schema(type_defs, mutation)
